import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import CoursesPage from "./pages/CoursesPage";
import StudentsPage from "./pages/StudentsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />

        <Route
          path="/dashboard"
          element={<DashboardPage />}
        />

        <Route
          path="/courses"
          element={<CoursesPage />}
        />

        <Route
          path="/students"
          element={<StudentsPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;