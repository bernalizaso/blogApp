import { useEffect, useState } from "react";
import { getAllEntriesAction } from "../actions/get-all-entries";
import type { Entry } from "../interfaces/EntryInterface";
import { postEntryAction } from "../actions/post-entry";

export const useEntries = () => {
  const [entries, setEntries] = useState<Entry[]>([]);

  const loadEntries = async () => {
    const data = await getAllEntriesAction();
    setEntries(data);
  };

  const postEntry = async (data: Entry) => {
    await postEntryAction(data);
    setEntries((prev) => [...prev, data]);
  };

  const filterEntries = async (query: string) => {
    const data = await getAllEntriesAction();
    const filtered = data.filter((element) =>
      element.content.toLowerCase().includes(query.toLowerCase()),
    );
    setEntries(filtered);
  };

  const addEntry = (newEntry: Entry) => {
    setEntries((prev) => [...prev, newEntry]);
  };

  useEffect(() => {
    loadEntries();
  }, []);

  return {
    entries,
    postEntry,
    filterEntries,
    addEntry,
    reload: loadEntries,
  };
};
