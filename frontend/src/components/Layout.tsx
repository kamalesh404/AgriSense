import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1 className="logo">AgriSense</h1>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/detect">Disease Detection</NavLink>
          <NavLink to="/crops">Crop Info</NavLink>
          <NavLink to="/weather">Weather Advice</NavLink>
        </nav>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
