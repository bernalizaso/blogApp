import { blogApp } from "../api/blog-api";
import type { Entry } from "../interfaces/EntryInterface";


export const postEntryAction= (async (data : Entry)=>{
await blogApp.post("/",data ) 
})