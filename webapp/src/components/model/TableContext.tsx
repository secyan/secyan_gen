import React from "react";
import { TableConfig } from "./table-config";

interface TableConfigContext {
  configs: TableConfig[];
  setConfigs(configs: TableConfig[]): void;
  openRawConfigDialog: boolean;
  setOpenRawConfigDialog(v: boolean): void;
}

//@ts-ignore
export const TableConfigContext = React.createContext<TableConfigContext>({});

export default function TableConfigProvider(props: any) {
  const { children } = props;

  const [configs, setConfigsState] = React.useState<TableConfig[]>([]);
  const [openRawConfigDialog, setOpenRawConfigDialog] = React.useState(false);

  React.useEffect(() => {
    let tableConfig = localStorage.getItem("tableStructure");
    if (tableConfig !== null) {
      setConfigsState(JSON.parse(tableConfig));
    }
  }, []);

  React.useEffect(() => {
    localStorage.setItem("tableStructure", JSON.stringify(configs));
  }, [configs]);

  const setConfigs = React.useCallback(
    (vs: TableConfig[]) => {
      localStorage.setItem("tableStructure", JSON.stringify(vs));
      setConfigsState(JSON.parse(JSON.stringify(vs)));
    },
    [configs]
  );

  const value: TableConfigContext = {
    configs,
    setConfigs,
    setOpenRawConfigDialog,
    openRawConfigDialog,
  };

  return (
    <TableConfigContext.Provider value={value}>
      {children}
    </TableConfigContext.Provider>
  );
}
