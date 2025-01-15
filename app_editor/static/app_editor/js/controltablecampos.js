function toggleTable(tableName) {
    // Pega a div de colunas da tabela com base no nome da tabela
    var tableDiv = document.getElementById(tableName);

    // Alterna a visibilidade da div
    if (tableDiv.style.display === "none") {
        tableDiv.style.display = "block";  // Expande
    } else {
        tableDiv.style.display = "none";  // Colapsa
    }
}

