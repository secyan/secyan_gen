import { message, notification } from "antd";
import axios from "axios";
import React from "react";
import { apiRoutes } from "../../settings/api_routes";
import { localStorageKeyConfig } from "../../settings/localstorage_keyconfig";
import { TableConfig } from "./table-config";
import { Utils } from "./utils/utils";

interface TableConfigContext {
  configs: TableConfig[];
  setConfigs(configs: TableConfig[], update?: boolean): void;
  openRawConfigDialog: boolean;
  setOpenRawConfigDialog(v: boolean): void;
  fetchConfigs(): Promise<void>;
}

//@ts-ignore
export const TableConfigContext = React.createContext<TableConfigContext>({});

export default function TableConfigProvider(props: any) {
  const { children } = props;

  const [configs, setConfigsState] = React.useState<TableConfig[]>([]);
  const [openRawConfigDialog, setOpenRawConfigDialog] = React.useState(false);

  React.useEffect(() => {
    let tableConfig = localStorage.getItem(
      localStorageKeyConfig.tableStructureKey
    );
    if (tableConfig !== null) {
      setConfigsState(JSON.parse(tableConfig));
    }
  }, []);

  React.useEffect(() => {
    localStorage.setItem(
      localStorageKeyConfig.tableStructureKey,
      JSON.stringify(configs)
    );
  }, [configs]);

  const setConfigs = React.useCallback(
    (vs: TableConfig[], update: boolean = true) => {
      localStorage.setItem(
        localStorageKeyConfig.tableStructureKey,
        JSON.stringify(vs)
      );
      if (update) {
        setConfigsState(JSON.parse(JSON.stringify(vs)));
      }
    },
    [configs]
  );

  const fetchConfigs = React.useCallback(async () => {
    try {
      let url = Utils.getURL(apiRoutes.fetchTableSchemaRoute);
      let resp = await axios.get(url);
      setConfigs(resp.data);
      message.success("Tables are updated");
    } catch (err) {
      notification.error({
        message: "Cannot fetch table configs",
        description: `${
          err?.response?.data ?? "Cannot connect to the backend"
        }`,
        duration: 5,
        placement: "bottomRight",
      });
    }
  }, []);

  const value: TableConfigContext = {
    configs,
    setConfigs,
    setOpenRawConfigDialog,
    openRawConfigDialog,
    fetchConfigs,
  };

  return (
    <TableConfigContext.Provider value={value}>
      {children}
    </TableConfigContext.Provider>
  );
}
