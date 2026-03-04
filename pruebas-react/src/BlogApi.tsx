import { BlogHeader } from "./components/BlogHeader";
import { BlogFooter } from "./components/BlogFooter";
import { EntriesList } from "./entries/EntriesList";
//import { Entries } from "./mock-entries/entries.mock";
import { getAllEntriesAction } from './actions/get-all-entries'
import { useState, useEffect } from "react";
import type { Entry } from "./interfaces/EntryInterface";
import { SearchComponent } from "./components/SearchComponent";
import { EntryForm } from "./components/EntryFormComponent";

export const BlogApp = () => {

  const [entries, setEntries] = useState<Entry[]>([]);

  const getEntriesFiltered = async (query: string) => {
    const Entries = await getAllEntriesAction()
    const filtered = Entries.filter((element) =>
      element.content.toLowerCase().includes(query.toLowerCase()),
    );

    setEntries(filtered);
  };


  useEffect(() => {
    async function getEntriesFromDB(){
      const data = await getAllEntriesAction()
      setEntries(data)
    }
    getEntriesFromDB()
  }, [getAllEntriesAction])
  
  

  const addEntry = (newEntry: Entry)=>{



    setEntries([...entries, newEntry]);

    console.log(entries)

  }

  return (
    <>
      <BlogHeader
        title="Blog de berni"
        subtitle="Este es un blog copa2"
      ></BlogHeader>
      <SearchComponent
        placeHolder="Busca la entrada"
        onQuery={getEntriesFiltered}
      ></SearchComponent>
      <EntriesList entries={entries} ></EntriesList>
      <EntryForm onSaveEntry={addEntry}></EntryForm>
      <BlogFooter msj="Copyright blablabla"></BlogFooter>
    </>
  );
};
