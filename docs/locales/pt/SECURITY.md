<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="security-policy"></a>
# Política de segurança

Relatar vulnerabilidades em particular para `security@onekit.org` com versão, plataforma, ferramenta, versões de dependência, impacto e reprodução sintética. Não publique arquivos sensíveis, credenciais ou relatórios privados prontos para explorar em rastreadores públicos. Conserta o alvo da última versão estável; nenhuma garantia de tempo de resposta está implícita.

O núcleo limita caminhos, tamanhos de entrada, expansão de arquivos, pixels de imagem, comparações e pipelines. Encriptação usa autenticada AES-256-GCM com sal fresco / nonce e scrypt; senhas perdidas não pode ser recuperado. As saídas existentes são preservadas por padrão. Python validação analisa a fonte sem executá-la.

Conversores/compiladores externos são programas nativos separados, não uma sandbox completa. Mantenha-os atualizados e isole documentos hostis usando controles OS. O CLI não é um serviço de conversão remota sem autenticação. A edição de um PDF assinado pode invalidar assinaturas; as permissões PDF não são equivalentes à integridade da criptografia.

Os cheques comuns nunca devem receber segredos de publicação. As etiquetas estáveis identificam commits protegidos-principais revisados. Dependência, licença e falhas de segurança bloqueiam a publicação. Nenhuma suíte de teste garante imunidade a todas as entradas ou ataques malformados.
