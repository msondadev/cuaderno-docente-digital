import { Link } from "react-router-dom";

export default function MainLayout({ children }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-slate-800 text-white p-4">
        <h1 className="text-xl font-bold mb-6">
          Cuaderno Docente
        </h1>

        <nav className="flex flex-col gap-3">
          <Link to="/dashboard">
            Dashboard
          </Link>

          <Link to="/courses">
            Cursos
          </Link>

          <Link to="/students">
            Alumnos
          </Link>
        </nav>
      </aside>

      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  );
}
