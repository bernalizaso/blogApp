import  { type KeyboardEvent, useState } from "react";

interface Props {
  placeHolder?: string;
  onQuery: (query: string) => void;
}

export const SearchComponent = ({ placeHolder, onQuery}: Props) => {
  const [query, setQuery] = useState("");
  const handleSearch = () => {
    if (query) {
        onQuery(query)
        setQuery("");
    }
  };
  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder={placeHolder}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button  onClick={handleSearch}>Buscar</button>
    </div>
  );
};
