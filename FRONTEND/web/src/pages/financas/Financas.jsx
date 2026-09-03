import "./Financas.css"

export default function Financas() {
    return (
        <div className="PaginaFinancas">
            <div className="Menu">
                <img
                    className="logo"
                    src="/assets/logoMinimal.png"
                />
                <img className="DaviIMG" src="/assets/davi.png" alt="" />
            </div>
        </div>
    )
}

// Tranformar essa porra toda em um componente de menu, e colocar o conteúdo da página dentro de outro componente, que vai ficar abaixo do menu.