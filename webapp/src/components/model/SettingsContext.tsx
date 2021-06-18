import { type } from "node:os";
import React from "react";

export type Role = "Client" | "Server";
export type BackEnd = "Default Backend" | "Postgres Backend";

interface Settings {
  role: Role;
  setRole(role: Role): void;
  backend: BackEnd;
  setBackend(b: BackEnd): void;
  datadir: string;
  setDatadir(v: string): void;
}

//@ts-ignore
export const SettingsContext = React.createContext<Settings>({});

export default function SettingsProvider(props: any) {
  const [role, setRoleState] = React.useState<Role>("Server");
  const [backend, setBackendState] = React.useState<BackEnd>("Default Backend");
  const [datadir, setDatadirState] = React.useState("");

  React.useEffect(() => {
    let role = localStorage.getItem("role");
    let backend = localStorage.getItem("");
    let data = localStorage.getItem("datadir");
    console.log(data);

    if (role) {
      setRoleState(role as Role);
    }
    if (backend) {
      setBackendState(backend as BackEnd);
    }

    if (data) {
      setDatadirState(data);
    }
  }, []);

  const setDatadir = React.useCallback((r: string) => {
    localStorage.setItem("datadir", r);
    setDatadirState(r);
  }, []);

  const setRole = React.useCallback((r: Role) => {
    localStorage.setItem("role", r);
    setRoleState(r);
  }, []);

  const setBackend = React.useCallback((r: BackEnd) => {
    localStorage.setItem("backend", r);
    setBackendState(r);
  }, []);

  const values: Settings = {
    role,
    setRole,
    backend,
    setBackend,
    datadir,
    setDatadir,
  };

  return (
    <SettingsContext.Provider value={values}>
      {props.children}
    </SettingsContext.Provider>
  );
}
