import { type } from "node:os";
import React from "react";

type Role = "Client" | "Server";

interface Settings {
  role: Role;
  setRole(role: Role): void;
}

//@ts-ignore
const SettingsContext = React.createContext<Settings>({});

export default function SettingsProvider(props: any) {
  const [role, setRoleState] = React.useState<Role>("Server");

  React.useEffect(() => {
    let role = localStorage.getItem("role");
    if (role) {
      setRoleState(role as Role);
    }
  }, []);

  const setRole = React.useCallback((r: Role) => {
    localStorage.setItem("role", role);
    setRoleState(role);
  }, []);

  const values: Settings = {
    role,
    setRole,
  };

  return (
    <SettingsContext.Provider value={values}>
      {props.children}
    </SettingsContext.Provider>
  );
}
