interface Props{
    msj : string;
}


export const BlogFooter = ({msj}:Props) => {
    return (
        <div>
            {msj}
        </div>
    )
}