import { useEffect, useState } from "react";
import { getAllEntriesAction } from "../actions/get-all-entries";
import type { Entry } from "../interfaces/EntryInterface";
import { postEntryAction } from "../actions/post-entry";
import { getEntryByIdAction } from "../actions/get-entry-by-id";
import { putEntryByIdAction } from "../actions/put-entry";

export const useEntries = () => {
  const [entries, setEntries] = useState<Entry[]>([]);




  const loadEntries = async () => {
    const data = await getAllEntriesAction();
    setEntries(data);
  };

  const getEntry= async(id:number)=>{
    const data = await getEntryByIdAction(id);
    return data
  }

  const postEntry = async (data: Entry) => {
    await postEntryAction(data);
    setEntries((prev) => [...prev, data]);
  };

  const putEntry = async (id:number, data: Entry) => {

    await putEntryByIdAction(id, data);
    await loadEntries(); 
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
    getEntry,
    filterEntries,
    addEntry,
    putEntry,
    reload: loadEntries,
  };
};
