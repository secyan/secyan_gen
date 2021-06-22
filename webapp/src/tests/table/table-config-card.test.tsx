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
