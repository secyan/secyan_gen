import React from "react";
import TableConfigCard from "../../components/pages/table/TableConfigCard";
import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import { SIMPLE_CONFIGS } from "../data/table-config-test";
import TableConfigProvider from "../../components/model/TableContext";
import { localStorageKeyConfig } from "../../settings/localstorage_keyconfig";
import { test_id_config } from "../data/test_id";
import TableConfigPage from "../../components/pages/table/TableConfigPage";
import { HashRouter as Router } from "react-router-dom";

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

test("Test simple card", async () => {
  render(
    <Router>
      <TableConfigProvider>
        <TableConfigPage />
      </TableConfigProvider>
    </Router>
  );

  let results = await screen.findAllByTestId(
    test_id_config.tableCard.testCardPathId
  );
  expect(results.length).toBe(SIMPLE_CONFIGS.length);
});
