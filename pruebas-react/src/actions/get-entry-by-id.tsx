import { blogApp } from "../api/blog-api";

export const getEntryByIdAction = async (id:number)=>{
    const response = await blogApp.get(`/${id}`,  )
    return response.data
}
