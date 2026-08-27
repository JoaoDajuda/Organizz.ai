import { Bar, Chart } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, scales, plugins } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

export default function GraficoFinanceiro({dados}) {
    // dados = [{ label: "Alimentação", valor: 46 }, ...]

    const chartData = {
        labels: dados.map((item) => item.label),
        datasets: [
            {
                data: dados.map((item) => item.valor),
                backgroundColor: "#E8B84B",
                borderRadius: 20,
                barThickness: 30,
            },
        ],
    };

    const chartOptions = {
        indexAxis: 'y',
        responsive: true,
        mintainAspectRatio: false,
        scales: {
            x: {
                min: 0,
                max: 100,
                display: false,
                grid: {display: false},
            },
            y: {
                display: false,
                grid: {display: false},
            }
        },
        plugins: {
            legend: { display: false },
            tooltip: { enabled: true}
        },
        backgroundColor: "#5A5A5A",
    }

    return <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", width: "50%", margin: "15px" }}>
      {dados.map((item, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <span style={{ color: "#fff", width: "100px" }}>{item.label}</span>
          <div style={{ flex: 1, position: "relative", height: "36px" }}>
            {/* trilho cinza de fundo */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                background: "#5A5A5A",
                borderRadius: "20px",
              }}
            />
            {/* barra dourada preenchida */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                width: `${item.valor}%`,
                background: "#E8B84B",
                borderRadius: "20px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#1a1a2e",
                fontWeight: 600,
                transition: "width 0.4s ease",
              }}
            >
              {item.valor}%
            </div>
          </div>
        </div>
      ))}
    </div>
}