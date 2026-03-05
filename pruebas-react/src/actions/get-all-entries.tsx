import { blogApp } from "../api/blog-api";
import type { Entry } from "../interfaces/EntryInterface"



export const getAllEntriesAction = async(): Promise<Entry[]> =>{
    const response = await blogApp.get<Entry[]>("/");

    return response.data
}

