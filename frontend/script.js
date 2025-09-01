const fileInput = document.getElementById('fileInput');
const emailText = document.getElementById('emailText');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');
const classifyBtn = document.getElementById('classify-btn');
const resultDiv = document.getElementById('result');
const categoriaP = document.getElementById('categoria');
const respostaP = document.getElementById('resposta');
const loadingDiv = document.getElementById('loading');

fileInput.addEventListener('change', handleFileUpload);
removeFile.addEventListener('click', clearSelectedFile);
classifyBtn.addEventListener('click', classificarEmail);

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';

    const fileType = file.name.split('.').pop().toLowerCase();

    if (fileType === 'txt') {
        readTextFile(file);
    } else if (fileType === 'pdf') {
        readPdfFile(file);
    } else {
        alert('Formato não suportado! Selecione um arquivo .txt ou .pdf');
        clearSelectedFile();
    }
}

function clearSelectedFile() {
    fileInput.value = '';
    fileInfo.style.display = 'none';
    emailText.value = '';
}

function readTextFile(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        emailText.value = e.target.result;
    };
    reader.readAsText(file);
}

function readPdfFile(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const typedArray = new Uint8Array(e.target.result);

        // Define a URL do worker do pdf.js. A URL abaixo está em um CDN.
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

        pdfjsLib.getDocument(typedArray).promise.then(pdf => {
            let text = '';
            const promises = [];

            for (let i = 1; i <= pdf.numPages; i++) {
                promises.push(
                    pdf.getPage(i).then(page => {
                        return page.getTextContent().then(content => {
                            const pageText = content.items.map(item => item.str).join(' ');
                            text += pageText + '\n';
                        });
                    })
                );
            }

            Promise.all(promises).then(() => {
                emailText.value = text.trim();
            });
        });
    };
    reader.readAsArrayBuffer(file);
}

async function classificarEmail() {
    const text = emailText.value.trim();

    if (!text) {
        alert('Por favor, insira um texto ou selecione um arquivo!');
        return;
    }

    // Esconder resultados e mostrar loading
    resultDiv.style.display = 'none';
    loadingDiv.style.display = 'flex';

    try {
        // A URL da API da Vercel agora aponta para o caminho correto
        const response = await fetch('/api/classify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email_content: text })
        });

        const data = await response.json();

        // Esconder loading
        loadingDiv.style.display = 'none';

        if (response.ok) {
            categoriaP.textContent = `Categoria: ${data.classification}`;
            respostaP.textContent = `Resposta sugerida: ${data.suggested_reply}`;
            resultDiv.style.display = 'block';
        } else {
            alert(`Erro do servidor: ${data.error || 'Ocorreu um erro.'}`);
        }

    } catch (error) {
        console.error('Erro na requisição:', error);
        loadingDiv.style.display = 'none';
        alert('Não foi possível se conectar ao servidor. Verifique se o backend está rodando.');
    }
}

function novaAnalise() {
    resultDiv.style.display = 'none';
}

function limparTudo() {
    emailText.value = '';
    clearSelectedFile();
    resultDiv.style.display = 'none';
}


