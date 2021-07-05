import React from "react";
import TableConfigCard from "../../components/pages/table/TableConfigCard";
import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import { SIMPLE_CONFIGS } from "../data/table-config-test";
import TableConfigProvider from "../../components/model/TableContext";
import { localStorageKeyConfig } from "../../settings/localstorage_keyconfig";
import { test_id_config } from "../data/test_id";

beforeAll(() => {
  jest.mock("monaco-editor/esm/vs/editor/editor.api.js");
});

beforeEach(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: jest.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(), // Deprecated
      removeListener: jest.fn(), // Deprecated
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
  localStorage.setItem(
    localStorageKeyConfig.tableStructureKey,
    JSON.stringify(SIMPLE_CONFIGS)
  );
});

afterEach(() => {
  localStorage.clear();
});

test("Test simple card", () => {
  render(
    <TableConfigProvider>
      <TableConfigCard config={SIMPLE_CONFIGS[0]} index={0} />
    </TableConfigProvider>
  );
  expect(
    screen.getByTestId(test_id_config.tableCard.testCardPathId)
  ).toHaveTextContent(SIMPLE_CONFIGS[0].data_paths[0]);

  expect(
    screen.getByTestId(test_id_config.tableCard.testCardSizeId)
  ).toHaveTextContent(SIMPLE_CONFIGS[0].data_sizes[0]);

  for (let column of SIMPLE_CONFIGS[0].columns) {
    expect(screen.getByDisplayValue(column.name)).toBeTruthy();
  }
});

test("Test simple card with annotation", () => {
  render(
    <TableConfigProvider>
      <TableConfigCard config={SIMPLE_CONFIGS[1]} index={1} />
    </TableConfigProvider>
  );
  expect(
    screen.getByTestId(test_id_config.tableCard.testCardPathId)
  ).toHaveTextContent(SIMPLE_CONFIGS[1].data_paths[0]);

  expect(
    screen.getByTestId(test_id_config.tableCard.testCardSizeId)
  ).toHaveTextContent(SIMPLE_CONFIGS[1].data_sizes[0]);

  expect(
    screen.getByDisplayValue(SIMPLE_CONFIGS[1].annotations[0])
  ).toBeTruthy();
});

test("Test Modify Annotation", () => {
  const config = SIMPLE_CONFIGS[1];
  render(
    <TableConfigProvider>
      <TableConfigCard config={config} index={1} />
    </TableConfigProvider>
  );
  let inputField = screen.getByDisplayValue(config.annotations[0]);
  fireEvent.change(inputField, { target: { value: "cde" } });
  expect(screen.getByDisplayValue("cde")).toBeTruthy();
  let newItem = localStorage.getItem(localStorageKeyConfig.tableStructureKey);
  expect(JSON.parse(newItem!)[1].annotations[0]).toBe("cde");
});

test("Test Modify field Name", async () => {
  const config = SIMPLE_CONFIGS[1];
  render(
    <TableConfigProvider>
      <TableConfigCard config={config} index={1} />
    </TableConfigProvider>
  );

  let fieldName = screen.getByDisplayValue(config.columns[0].name);
  fireEvent.change(fieldName, { target: { value: "abcd" } });
  expect(screen.getByDisplayValue("abcd")).toBeTruthy();
  let newItem = localStorage.getItem(localStorageKeyConfig.tableStructureKey);
  expect(JSON.parse(newItem!)[1].columns[0].name).toBe("abcd");
});
