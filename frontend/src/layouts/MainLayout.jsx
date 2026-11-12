import { Link, useLocation, useNavigate } from "react-router-dom";
import { BookOpen, LayoutDashboard, GraduationCap, Users, LogOut } from "lucide-react";

export default function MainLayout({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  const navItems = [
    { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { path: "/courses", label: "Cursos", icon: GraduationCap },
    { path: "/students", label: "Alumnos", icon: Users },
  ];

  return (
    <div className="flex min-h-screen bg-slate-100">
      {/* Sidebar Fija */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col justify-between p-4 shadow-xl">
        <div>
          <div className="flex items-center gap-3 px-2 py-4 mb-6 border-b border-slate-800">
            <BookOpen className="text-blue-500" size={28} />
            <span className="font-bold text-lg tracking-wide">CuadernoDocente</span>
          </div>

          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-blue-600 text-white"
                      : "text-slate-400 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <Icon size={18} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Perfil de Usuario y Logout */}
        <div className="border-t border-slate-800 pt-4 mt-auto">
          <div className="px-3 py-2">
            <p className="text-xs text-slate-400">Usuario activo</p>
            <p className="text-sm font-medium text-white truncate">
              {user.usuario || "Docente"}
            </p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full mt-2 flex items-center gap-2 px-3 py-2 text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
          >
            <LogOut size={18} />
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Contenido Principal */}
      <main className="flex-1 p-8 overflow-y-auto">{children}</main>
    </div>
  );
}
