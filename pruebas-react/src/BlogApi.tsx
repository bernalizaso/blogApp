import { BlogHeader } from "./components/BlogHeader";
import { BlogFooter } from "./components/BlogFooter";
import { EntriesList } from "./components/EntriesList";
import { SearchComponent } from "./components/SearchComponent";
import { EntryForm } from "./components/EntryFormComponent";
import { useEntries} from "./hooks/useEntries"

export const BlogApp = () => {
  const { entries, filterEntries, postEntry } = useEntries();

  return (
    <>
      <BlogHeader
        title="Blog de berni"
        subtitle="Este es un blog copa2"
      ></BlogHeader>
      <SearchComponent
        placeHolder="Busca la entrada"
        onQuery={filterEntries}
      ></SearchComponent>
      <EntriesList entries={entries} ></EntriesList>
      <EntryForm onSaveEntry={postEntry}></EntryForm>
      <BlogFooter msj="Copyright blablabla"></BlogFooter>
    </>
  );
};
