import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import {
  BellIcon,
  BookIcon,
  CalendarIcon,
  CloseIcon,
  GlobeIcon,
  LeafIcon,
  MenuIcon,
  SproutIcon,
  SunIcon,
  UploadIcon,
} from "./Icons";

type Lang = "en" | "ta";

const T: Record<Lang, Record<string, string>> = {
  en: {
    dashboard: "Dashboard",
    detect: "Disease Detection",
    diseases: "Disease Encyclopedia",
    crops: "Crop Info",
    recommendations: "Smart Recommendations",
    weather: "Weather Dashboard",
  },
  ta: {
    dashboard: "டாஷ்போர்டு",
    detect: "நோய் கண்டறிதல்",
    diseases: "நோய் அகராதி",
    crops: "பயிர் தகவல்",
    recommendations: "புத்திசாலி பரிந்துரைகள்",
    weather: "வானிலை டாஷ்போர்டு",
  },
};

const NAV: { to: string; key: keyof (typeof T)["en"]; end?: boolean }[] = [
  { to: "/", key: "dashboard", end: true },
  { to: "/detect", key: "detect" },
  { to: "/diseases", key: "diseases" },
  { to: "/crops", key: "crops" },
  { to: "/recommendations", key: "recommendations" },
  { to: "/weather", key: "weather" },
];

const NAV_ICONS: Record<string, (className: string) => JSX.Element> = {
  dashboard: (c) => <SproutIcon className={c} />,
  detect: (c) => <UploadIcon className={c} />,
  diseases: (c) => <BookIcon className={c} />,
  crops: (c) => <LeafIcon className={c} />,
  recommendations: (c) => <CalendarIcon className={c} />,
  weather: (c) => <SunIcon className={c} />,
};

const NOTIFICATIONS = [
  {
    id: 1,
    title: "Weather Alert",
    body: "Heavy rainfall expected in 48 hours. Check drainage in low-lying fields.",
    time: "2h ago",
    severity: "warning" as const,
  },
  {
    id: 2,
    title: "Disease Outbreak Watch",
    body: "Humidity above 85% for 3 consecutive days raises blight risk.",
    time: "6h ago",
    severity: "critical" as const,
  },
  {
    id: 3,
    title: "Irrigation Reminder",
    body: "Soil moisture is below optimal. Schedule irrigation for early morning.",
    time: "1d ago",
    severity: "info" as const,
  },
];

export default function Layout() {
  const [lang, setLang] = useState<Lang>("en");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [readIds, setReadIds] = useState<Set<number>>(new Set());

  const unread = NOTIFICATIONS.filter((n) => !readIds.has(n.id)).length;
  const t = T[lang];

  const markAllRead = () => {
    setReadIds(new Set(NOTIFICATIONS.map((n) => n.id)));
  };

  return (
    <div className="layout">
      <button
        className="hamburger"
        aria-label="Toggle navigation menu"
        onClick={() => setSidebarOpen((o) => !o)}
      >
        {sidebarOpen ? <CloseIcon /> : <MenuIcon />}
      </button>

      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="brand">
          <span className="brand-icon">
            <SproutIcon width={26} height={26} />
          </span>
          <div>
            <h1 className="logo">AgriSense</h1>
            <span className="brand-tag">AI Farm Intelligence</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
              onClick={() => setSidebarOpen(false)}
            >
              {NAV_ICONS[item.key]("nav-icon")}
              <span>{t[item.key]}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button
            className="lang-toggle"
            onClick={() => setLang((l) => (l === "en" ? "ta" : "en"))}
            aria-label="Toggle language between English and Tamil"
          >
            <GlobeIcon className="nav-icon" />
            <span>{lang === "en" ? "English" : "Tamil"}</span>
            <span className="lang-pill">{lang === "en" ? "TA" : "EN"}</span>
          </button>
        </div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div className="topbar-spacer" />
          <div className="topbar-actions">
            <div className="notif-wrap">
              <button
                className="icon-btn"
                aria-label="View notifications"
                onClick={() => setNotifOpen((o) => !o)}
              >
                <BellIcon />
                {unread > 0 && <span className="notif-dot" />}
              </button>
              {notifOpen && (
                <div className="notif-panel">
                  <div className="notif-header">
                    <strong>Notifications</strong>
                    <button className="link-btn" onClick={markAllRead}>
                      Mark all read
                    </button>
                  </div>
                  {NOTIFICATIONS.map((n) => (
                    <div key={n.id} className="notif-item">
                      <span className={`notif-sev sev-${n.severity}`} />
                      <div className="notif-body">
                        <strong>{n.title}</strong>
                        <p>{n.body}</p>
                        <span className="notif-time">{n.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div className="lang-switch">
              <button
                className={lang === "en" ? "lang-btn active" : "lang-btn"}
                onClick={() => setLang("en")}
              >
                EN
              </button>
              <button
                className={lang === "ta" ? "lang-btn active" : "lang-btn"}
                onClick={() => setLang("ta")}
              >
                TA
              </button>
            </div>
          </div>
        </header>

        <Outlet />
      </main>
    </div>
  );
}
