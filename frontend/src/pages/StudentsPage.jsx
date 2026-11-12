import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import api from "../services/api";
import { UserPlus, UserCheck, Search, Mail } from "lucide-react";

export default function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const [showStudentModal, setShowStudentModal] = useState(false);
  const [showEnrollModal, setShowEnrollModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);

  // Formularios
  const [studentForm, setStudentForm] = useState({ nombre: "", apellido: "", email: "" });
  const [enrollForm, setEnrollForm] = useState({ id_curso: "", estado_academico: "REGULAR" });

  const fetchData = async () => {
    try {
      const [resStudents, resCourses] = await Promise.all([
        api.get("/students/"),
        api.get("/courses/"),
      ]);
      setStudents(resStudents.data);
      setCourses(resCourses.data);
    } catch (err) {
      console.error("Error al cargar alumnos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    try {
      await api.post("/students/", studentForm);
      setShowStudentModal(false);
      setStudentForm({ nombre: "", apellido: "", email: "" });
      fetchData();
    } catch (err) {
      alert("Error al registrar alumno");
    }
  };

  const handleEnrollStudent = async (e) => {
    e.preventDefault();
    if (!selectedStudent || !enrollForm.id_curso) return;

    try {
      await api.post("/inscriptions/", {
        id_alumno: selectedStudent.id_alumno,
        id_curso: parseInt(enrollForm.id_curso),
        fecha_inscripcion: new Date().toISOString().split("T"),
        estado_academico: enrollForm.estado_academico,
      });
      setShowEnrollModal(false);
      alert("Alumno inscripto correctamente en el curso");
    } catch (err) {
      alert("Error al inscribir alumno: " + (err.response?.data?.detail || err.message));
    }
  };

  const filteredStudents = students.filter(
    (s) =>
      s.nombre.toLowerCase().includes(search.toLowerCase()) ||
      s.apellido.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <MainLayout>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Nómina de Alumnos</h1>
          <p className="text-slate-500 text-sm mt-1">
            Gestión de estudiantes e inscripciones por materia
          </p>
        </div>
        <button
          onClick={() => setShowStudentModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg flex items-center gap-2 font-medium shadow-md transition"
        >
          <UserPlus size={18} />
          Nuevo Alumno
        </button>
      </div>

      {/* Buscador */}
      <div className="mb-6 relative max-w-md">
        <Search className="absolute left-3 top-3 text-slate-400" size={18} />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Buscar por nombre o apellido..."
          className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500 shadow-sm"
        />
      </div>

      {loading ? (
        <p className="text-slate-500">Cargando alumnos...</p>
      ) : (
        <div className="bg-white border rounded-xl overflow-hidden shadow-sm">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                <th className="p-4">ID</th>
                <th className="p-4">Alumno</th>
                <th className="p-4">Email</th>
                <th className="p-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y text-sm text-slate-700">
              {filteredStudents.length === 0 ? (
                <tr>
                  <td colSpan="4" className="p-4 text-center text-slate-400">
                    No se encontraron alumnos registrados.
                  </td>
                </tr>
              ) : (
                filteredStudents.map((s) => (
                  <tr key={s.id_alumno} className="hover:bg-slate-50/50">
                    <td className="p-4 font-mono text-slate-400 text-xs">#{s.id_alumno}</td>
                    <td className="p-4 font-semibold text-slate-800">
                      {s.apellido}, {s.nombre}
                    </td>
                    <td className="p-4 text-slate-500">
                      {s.email ? (
                        <span className="flex items-center gap-1.5">
                          <Mail size={14} className="text-slate-400" />
                          {s.email}
                        </span>
                      ) : (
                        <span className="text-slate-300 italic">Sin correo</span>
                      )}
                    </td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => {
                          setSelectedStudent(s);
                          setShowEnrollModal(true);
                        }}
                        className="inline-flex items-center gap-1 text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 text-slate-600 font-medium px-3 py-1.5 rounded-md transition"
                      >
                        <UserCheck size={14} />
                        Inscribir a Curso
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal Nuevo Alumno */}
      {showStudentModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6 shadow-2xl">
            <h2 className="text-xl font-bold text-slate-800 mb-4">Registrar Alumno</h2>
            <form onSubmit={handleCreateStudent} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Nombre</label>
                <input
                  type="text"
                  required
                  value={studentForm.nombre}
                  onChange={(e) => setStudentForm({ ...studentForm, nombre: e.target.value })}
                  placeholder="Ej: Carlos"
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Apellido</label>
                <input
                  type="text"
                  required
                  value={studentForm.apellido}
                  onChange={(e) => setStudentForm({ ...studentForm, apellido: e.target.value })}
                  placeholder="Ej: Gómez"
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Email de Contacto</label>
                <input
                  type="email"
                  value={studentForm.email}
                  onChange={(e) => setStudentForm({ ...studentForm, email: e.target.value })}
                  placeholder="carlos.gomez@alumno.edu.ar"
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowStudentModal(false)}
                  className="px-4 py-2 border text-slate-600 rounded-lg text-sm hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                >
                  Guardar Alumno
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Inscribir a Curso */}
      {showEnrollModal && selectedStudent && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6 shadow-2xl">
            <h2 className="text-xl font-bold text-slate-800 mb-1">Inscribir Alumno</h2>
            <p className="text-xs text-slate-500 mb-4">
              Estudiante: <span className="font-bold text-slate-700">{selectedStudent.apellido}, {selectedStudent.nombre}</span>
            </p>
            <form onSubmit={handleEnrollStudent} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Seleccionar Curso</label>
                <select
                  required
                  value={enrollForm.id_curso}
                  onChange={(e) => setEnrollForm({ ...enrollForm, id_curso: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2 text-sm bg-white"
                >
                  <option value="">-- Seleccione un curso --</option>
                  {courses.map((c) => (
                    <option key={c.id_curso} value={c.id_curso}>
                      {c.materia} ({c.division} - {c.institucion})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Estado Académico Inicial</label>
                <select
                  value={enrollForm.estado_academico}
                  onChange={(e) => setEnrollForm({ ...enrollForm, estado_academico: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2 text-sm bg-white"
                >
                  <option value="REGULAR">REGULAR</option>
                  <option value="LIBRE">LIBRE</option>
                  <option value="PROMOVIDO">PROMOVIDO</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowEnrollModal(false)}
                  className="px-4 py-2 border text-slate-600 rounded-lg text-sm hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                >
                  Confirmar Inscripción
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </MainLayout>
  );
}
