<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

Lançamento inicial do offline CLI e Python processamento API com 230 ferramentas para documentos, PDFs, imagens, mídia, arquivos, fontes, utilitários de desenvolvimento, códigos QR, declarações de licença e inspeção de arquivos. A instalação de base não tem dependências de execução; extras opcionais e motores externos habilitam as ferramentas selecionadas.

Inclui validação de entrada limitada, fluxos de trabalho reutilizáveis, configuração de dependência local, contratos de processamento específicos de formato e inspeção de licença baseada em fonte. Relatórios de licença permanecem estimativas não verificadas que requerem revisão manual.

Atualizações de desempenho aceleram a preparação de imagens opacas e inspeção de texto. Importações não utilizadas e atribuições redundantes de motores de desenvolvimento foram removidas.

Motores modelo são opcionais: instalar o `background` ou `transcription` extra quando necessário. O U2Net é executado diretamente com ONNX Runtime e um modelo de cache verificado por somas. Whisper usa faster-whisper. Os arquivos permanecem locais; os pesos do modelo de download da primeira execução. O processamento de vídeo requer FFmpeg e ffprobe. O download de vídeo usa o separado `video` extra.

Atualizações Pillow para 13 e o bloqueio certificado para endereço de avisos publicados. O extra portátil `all` permanece separado dos motores modelo e assinatura.
