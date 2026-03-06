import { useState, useEffect } from "react";
import type { Entry } from "../interfaces/EntryInterface";
import { getEntryByIdAction } from "../actions/get-entry-by-id";
import { putEntryByIdAction } from "../actions/put-entry";
import { useEntries} from '../hooks/useEntries'


//{onSuccess}:Props
export const EntryFormEdit = () => {
  const { getEntry, putEntry } = useEntries();
  
  const [formId, setFormId] = useState("");
  const [formTitle, setFormTitle] = useState("");
  const [formBody, setFormBody] = useState("");
  const [formDate, setFormDate] = useState("");
  
  const [isEditing, setIsEditing] = useState(false);

  // Acción para buscar los datos existentes
  const handleLoadEntry = async () => {
    if (!formId) return;
    const entry: Entry = await getEntry(Number(formId));
    
    setFormTitle(entry.tittle);
    setFormBody(entry.content);
    setFormDate(entry.date);
    setIsEditing(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const updatedEntry: Entry = {
      id: Number(formId),
      tittle: formTitle,
      content: formBody,
      date: formDate,
    };

    await putEntry(Number(formId), updatedEntry);
    alert("¡Editado con éxito!");
    setIsEditing(false); 
  };

  return (
    <div>
      <section>
        <input 
          type="number" 
          placeholder="ID a editar" 
          value={formId} 
          onChange={(e) => setFormId(e.target.value)}
          disabled={isEditing} 
        />
        {!isEditing && <button onClick={handleLoadEntry}>Cargar Datos</button>}
      </section>

      {isEditing && (
        <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
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
          <button type="submit">Guardar Cambios (PUT)</button>
          <button type="button" onClick={() => setIsEditing(false)}>Cancelar</button>
        </form>
      )}
    </div>
  );
};