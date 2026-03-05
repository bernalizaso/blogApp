import type { Entry } from "../interfaces/EntryInterface";
import type { FC } from "react";

interface Props {
  entries: Entry[];

}

export const EntriesList: FC<Props> = ({ entries }) => {

  return (
    <div>
      {entries.map((Entry) => (
        <div>
          <h1>{Entry.tittle}</h1>
          <h3>{Entry.content}</h3>
          <h5>{Entry.date}</h5>
        </div>
      ))}
    </div>
  );
};
