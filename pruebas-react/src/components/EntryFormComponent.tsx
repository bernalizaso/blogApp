import type { Entry } from "../interfaces/EntryInterface";

import { useState } from "react";

interface Props {
  onSaveEntry: (newEntry: Entry) => void;
}
export const EntryForm = ({ onSaveEntry }: Props) => {
  const [formTitle, setFormTitle] = useState("");
  const [formBody, setFormBody] = useState("");
  const [formDate, setFormDate] = useState("");
  const [formId, setFormId] = useState("");

  const handleSubmit = (e: any) => {
    e.preventDefault();

    const newEntry: Entry = {
      id: Number(formId),
      tittle: formTitle,
      content: formBody,
      date: formDate,
    };

    onSaveEntry(newEntry);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Título"
        value={formTitle}
        onChange={(e) => setFormTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Cuerpo"
        value={formBody}
        onChange={(e) => setFormBody(e.target.value)}
      />
      <input
        type="date"
        value={formDate}
        onChange={(e) => setFormDate(e.target.value)}
      />
      <input
        type="number"
        placeholder="ID"
        value={formId}
        onChange={(e) => setFormId(e.target.value)}
      />
      <button type="submit">Guardar</button>
    </form>
  );
};
