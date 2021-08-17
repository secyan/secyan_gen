/** @format */

import { message, notification } from "antd";
import axios from "axios";
import React from "react";
import { apiRoutes } from "../../settings/api_routes";
import { localStorageKeyConfig } from "../../settings/localstorage_keyconfig";
import { TableConfig } from "./table-config";
import { Utils } from "./utils/utils";

export type Role = "Client" | "Server";
export type BackEnd = "Default Backend" | "Postgres Backend";

interface Settings {
  loaded: boolean;
  role: Role;
  setRole(role: Role): void;
  backend: BackEnd;
  setBackend(b: BackEnd): void;
  datadir: string;
  setDatadir(v: string): void;
  isDownloading: boolean;
  downloadData(configs: TableConfig[]): Promise<TableConfig[] | undefined>;
}

//@ts-ignore
export const SettingsContext = React.createContext<Settings>({});

export default function SettingsProvider(props: any) {
  const [loaded, setLoaded] = React.useState(false);
  const [role, setRoleState] = React.useState<Role>("Server");
  const [backend, setBackendState] = React.useState<BackEnd>("Default Backend");
  const [datadir, setDatadirState] = React.useState("");
  const [isDownloading, setIsDownloading] = React.useState(false);

  React.useEffect(() => {
    let role = localStorage.getItem(localStorageKeyConfig.roleKey);
    let backend = localStorage.getItem(localStorageKeyConfig.backendKey);
    let data = localStorage.getItem(localStorageKeyConfig.datadirKey);

    if (role) {
      setRoleState(role as Role);
    }
    if (backend) {
      setBackendState(backend as BackEnd);
    }

    if (data) {
      setDatadirState(data);
    }

    setLoaded(true);
  }, []);

  const setDatadir = React.useCallback((r: string) => {
    localStorage.setItem(localStorageKeyConfig.datadirKey, r);
    setDatadirState(r);
  }, []);

  const setRole = React.useCallback((r: Role) => {
    localStorage.setItem(localStorageKeyConfig.roleKey, r);
    setRoleState(r);
  }, []);

  const setBackend = React.useCallback((r: BackEnd) => {
    localStorage.setItem(localStorageKeyConfig.backendKey, r);
    setBackendState(r);
  }, []);

  const downloadData = React.useCallback(
    async (configs: TableConfig[]): Promise<TableConfig[] | undefined> => {
      setIsDownloading(true);
      try {
        let url = Utils.getURL(apiRoutes.downloadDataRoute);
        let data = await axios.post(url, {
          tables: JSON.stringify(configs),
          output_dir: datadir,
        });
        message.success("Successfully dump data into " + datadir, 8);
        return data.data;
      } catch (err) {
        notification.error({
          message: "Cannot fetch table configs",
          description: `${
            err?.response?.data ?? "Cannot connect to the backend"
          }`,
          duration: 5,
          placement: "bottomRight",
        });
        return undefined;
      } finally {
        setIsDownloading(false);
      }
    },
    [datadir]
  );

  const values: Settings = {
    role,
    setRole,
    backend,
    setBackend,
    datadir,
    setDatadir,
    loaded,
    isDownloading,
    downloadData,
  };

  return (
    <SettingsContext.Provider value={values}>
      {props.children}
    </SettingsContext.Provider>
  );
}
