import type { Entry } from "../interfaces/EntryInterface";
import { blogApp } from "../api/blog-api";

export const putEntryByIdAction = async (id: number, data: Entry) => {
  const response =await blogApp.put(`/${id}`,  data );

  return response.data

};
