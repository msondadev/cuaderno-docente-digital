import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import api from "../services/api";
import { Plus, GraduationCap, Folder } from "lucide-react";

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // 1. Lectura dinámica del usuario autenticado desde localStorage
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const docenteId = user.id_usuario || user.id;

  // 2. Estado inicial del formulario sin id_docente hardcodeado
  const [formData, setFormData] = useState({
    materia: "",
    division: "",
    institucion: "",
    regimen: "SECUNDARIA",
    max_faltas: 20,
    porcentaje_minimo: 75,
    enlace_drive: "",
  });

  const fetchCourses = async () => {
    try {
      const res = await api.get("/courses/");
      setCourses(res.data);
    } catch (err) {
      console.error("Error al cargar cursos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!docenteId) {
      alert("No se detectó la sesión del docente. Por favor, cierra sesión e ingresa nuevamente.");
      return;
    }

    try {
      // 3. Inyección explícita del id_docente de la sesión en el objeto payload
      const payload = {
        ...formData,
        id_docente: docenteId,
      };

      // Envío del payload correcto a FastAPI
      await api.post("/courses/", payload);

      setShowModal(false);
      setFormData({
        materia: "",
        division: "",
        institucion: "",
        regimen: "SECUNDARIA",
        max_faltas: 20,
        porcentaje_minimo: 75,
        enlace_drive: "",
      });
      fetchCourses();
    } catch (err) {
      alert("Error al crear el curso: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <MainLayout>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Cursos Asignados</h1>
          <p className="text-slate-500 text-sm mt-1">
            Administra tus materias y configuraciones de faltas
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg flex items-center gap-2 font-medium shadow-md transition"
        >
          <Plus size={18} />
          Nuevo Curso
        </button>
      </div>

      {loading ? (
        <p className="text-slate-500">Cargando materias...</p>
      ) : courses.length === 0 ? (
        <div className="bg-white border rounded-xl p-8 text-center text-slate-500">
          <GraduationCap size={48} className="mx-auto text-slate-300 mb-3" />
          <p className="text-lg font-medium">No tienes cursos registrados aún</p>
          <p className="text-sm">Haz clic en "Nuevo Curso" para comenzar</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <div
              key={course.id_curso}
              className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start mb-3">
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded">
                    {course.regimen}
                  </span>
                  <span className="text-xs text-slate-400 font-medium">
                    División: {course.division}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-1">
                  {course.materia}
                </h3>
                <p className="text-sm text-slate-500 mb-4">{course.institucion}</p>

                <div className="bg-slate-50 p-3 rounded-lg text-xs space-y-1.5 text-slate-600 mb-4">
                  <div className="flex justify-between">
                    <span>Límite Faltas:</span>
                    <span className="font-semibold text-slate-800">{course.max_faltas}</span>
                  </div>
                  {course.porcentaje_minimo && (
                    <div className="flex justify-between">
                      <span>Asistencia Mínima:</span>
                      <span className="font-semibold text-slate-800">{course.porcentaje_minimo}%</span>
                    </div>
                  )}
                </div>
              </div>

              {course.enlace_drive && (
                <a
                  href={course.enlace_drive}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-2 text-xs text-blue-600 hover:underline mb-2"
                >
                  <Folder size={14} />
                  Carpeta de Google Drive
                </a>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Modal para alta de nuevo curso */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6 shadow-2xl">
            <h2 className="text-xl font-bold text-slate-800 mb-4">Crear Nuevo Curso</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Materia</label>
                <input
                  type="text"
                  required
                  value={formData.materia}
                  onChange={(e) => setFormData({ ...formData, materia: e.target.value })}
                  placeholder="Ej: Gestión de Proyectos"
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">División / Año</label>
                  <input
                    type="text"
                    required
                    value={formData.division}
                    onChange={(e) => setFormData({ ...formData, division: e.target.value })}
                    placeholder="Ej: 3° A"
                    className="w-full border rounded-lg px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">Régimen</label>
                  <select
                    value={formData.regimen}
                    onChange={(e) => setFormData({ ...formData, regimen: e.target.value })}
                    className="w-full border rounded-lg px-3 py-2 text-sm bg-white"
                  >
                    <option value="SECUNDARIA">Secundaria</option>
                    <option value="TERCIARIO">Terciario</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Institución</label>
                <input
                  type="text"
                  required
                  value={formData.institucion}
                  onChange={(e) => setFormData({ ...formData, institucion: e.target.value })}
                  placeholder="Ej: ISFT N° 12"
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">Max Faltas</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    value={formData.max_faltas}
                    onChange={(e) => setFormData({ ...formData, max_faltas: parseFloat(e.target.value) })}
                    className="w-full border rounded-lg px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 mb-1">% Mínimo Asistencia</label>
                  <input
                    type="number"
                    value={formData.porcentaje_minimo || ""}
                    onChange={(e) => setFormData({ ...formData, porcentaje_minimo: parseFloat(e.target.value) })}
                    placeholder="Ej: 75"
                    className="w-full border rounded-lg px-3 py-2 text-sm"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Enlace Google Drive (Opcional)</label>
                <input
                  type="url"
                  value={formData.enlace_drive}
                  onChange={(e) => setFormData({ ...formData, enlace_drive: e.target.value })}
                  placeholder="https://drive.google.com/..."
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border text-slate-600 rounded-lg text-sm hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                >
                  Guardar Curso
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </MainLayout>
  );
}
