import { Entries } from "../mock-entries/entries.mock";


export const getEntry = ( id : number)=>{
    Entries.forEach(element => {
        if (element.id === id){
            return element
        }
        else{ return}
    }); 
}