#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Envio de Email Marketing - CEPEO
Author: Lucas Henrique
Date: 2025-10-09

Este script lê os contatos de um arquivo CSV e envia emails marketing
personalizados usando um template HTML com imagens incorporadas.
"""

import os
import sys
import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class EmailMarketingCEPEO:
    """Classe para gerenciar o envio de emails marketing da CEPEO"""

    def __init__(self):
        """Inicializa a classe com as configurações do .env"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_name = os.getenv("FROM_NAME", "CEPEO")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
        self.email_subject = os.getenv("EMAIL_SUBJECT", "CEPEO - Produtos em Destaque")

        # Validar credenciais
        if not self.email_user or not self.email_password:
            raise ValueError(
                "❌ EMAIL_USER e EMAIL_PASSWORD devem estar configurados no arquivo .env"
            )

        # Caminhos dos arquivos
        self.base_path = Path(__file__).parent
        self.csv_file = self.base_path / "contato.csv"
        self.html_template = self.base_path / "email.html"
        self.logo_path = self.base_path / "arquivos" / "logo_cepeo.jpeg"
        self.produto1_path = self.base_path / "arquivos" / "produto-1.jpeg"
        self.produto2_path = self.base_path / "arquivos" / "produto-2.jpeg"

        # Verificar se os arquivos existem
        self._verificar_arquivos()

    def _verificar_arquivos(self):
        """Verifica se todos os arquivos necessários existem"""
        arquivos_necessarios = {
            "CSV de contatos": self.csv_file,
            "Template HTML": self.html_template,
            "Logo CEPEO": self.logo_path,
            "Produto 1": self.produto1_path,
            "Produto 2": self.produto2_path,
        }

        arquivos_faltando = []
        for nome, caminho in arquivos_necessarios.items():
            if not caminho.exists():
                arquivos_faltando.append(f"  - {nome}: {caminho}")

        if arquivos_faltando:
            print("❌ Arquivos não encontrados:")
            print("\n".join(arquivos_faltando))
            sys.exit(1)

    def ler_contatos(self):
        """Lê os contatos do arquivo CSV"""
        contatos = []
        try:
            with open(self.csv_file, "r", encoding="utf-8") as file:
                # O CSV usa ponto e vírgula como separador
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    nome = row.get("Nome", "").strip()
                    email = row.get("Email", "").strip()

                    # Formatar nome para Title Case (primeira letra maiúscula)
                    nome_formatado = nome.title() if nome else ""

                    # Validação básica
                    if nome_formatado and email and "@" in email:
                        contatos.append({"nome": nome_formatado, "email": email})

            print(f"✅ {len(contatos)} contatos válidos carregados do CSV")
            return contatos

        except Exception as e:
            print(f"❌ Erro ao ler o arquivo CSV: {e}")
            sys.exit(1)

    def carregar_template_html(self, nome_destinatario):
        """Carrega o template HTML e personaliza com o nome do destinatário"""
        try:
            with open(self.html_template, "r", encoding="utf-8") as file:
                html_content = file.read()

            # Substituir o placeholder {nome} pelo nome real
            html_personalizado = html_content.replace("{nome}", nome_destinatario)
            return html_personalizado

        except Exception as e:
            print(f"❌ Erro ao carregar template HTML: {e}")
            sys.exit(1)

    def criar_mensagem_email(self, destinatario_email, destinatario_nome):
        """Cria a mensagem de email com HTML e imagens incorporadas"""
        msg = MIMEMultipart("related")
        msg["Subject"] = self.email_subject
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = destinatario_email

        # Parte alternativa para suportar HTML
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)

        # Carregar e anexar o HTML personalizado
        html_content = self.carregar_template_html(destinatario_nome)
        msg_html = MIMEText(html_content, "html", "utf-8")
        msg_alternative.attach(msg_html)

        # Anexar as imagens como inline (CID)
        imagens = {
            "logo_cepeo": self.logo_path,
            "produto_1": self.produto1_path,
            "produto_2": self.produto2_path,
        }

        for cid, caminho_imagem in imagens.items():
            try:
                with open(caminho_imagem, "rb") as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header("Content-ID", f"<{cid}>")
                    img.add_header(
                        "Content-Disposition", "inline", filename=caminho_imagem.name
                    )
                    msg.attach(img)
            except Exception as e:
                print(f"⚠️  Aviso: Erro ao anexar imagem {cid}: {e}")

        return msg

    def enviar_email(self, destinatario_email, destinatario_nome):
        """Envia um email para um destinatário específico"""
        try:
            # Criar a mensagem
            msg = self.criar_mensagem_email(destinatario_email, destinatario_nome)

            # Conectar ao servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Ativar TLS
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"❌ Erro ao enviar email para {destinatario_email}: {e}")
            return False

    def enviar_campanha(self, limite=None, delay=1):
        """
        Envia a campanha de email marketing para todos os contatos

        Args:
            limite (int): Número máximo de emails a enviar (None = todos)
            delay (float): Tempo de espera entre envios em segundos
        """
        print("=" * 60)
        print("📧 SISTEMA DE EMAIL MARKETING - CEPEO")
        print("=" * 60)
        print()

        # Ler contatos
        contatos = self.ler_contatos()

        if not contatos:
            print("❌ Nenhum contato válido encontrado!")
            return

        # Aplicar limite se especificado
        if limite and limite < len(contatos):
            contatos = contatos[:limite]
            print(
                f"⚠️  Modo de teste: enviando apenas para os primeiros {limite} contatos"
            )

        # Confirmação do usuário
        print(f"\n📊 Resumo da campanha:")
        print(f"   - Total de destinatários: {len(contatos)}")
        print(f"   - Servidor SMTP: {self.smtp_server}")
        print(f"   - Remetente: {self.from_name} <{self.from_email}>")
        print(f"   - Assunto: {self.email_subject}")
        print()

        resposta = input("Deseja continuar com o envio? (s/n): ").strip().lower()
        if resposta != "s":
            print("❌ Envio cancelado pelo usuário.")
            return

        print("\n🚀 Iniciando envio de emails...\n")

        # Estatísticas
        enviados = 0
        falhas = 0

        # Enviar emails
        for i, contato in enumerate(contatos, 1):
            nome = contato["nome"]
            email = contato["email"]

            print(f"[{i}/{len(contatos)}] Enviando para: {nome} ({email})...", end=" ")

            if self.enviar_email(email, nome):
                print("✅ Sucesso!")
                enviados += 1
            else:
                print("❌ Falha!")
                falhas += 1

            # Aguardar entre envios (evitar bloqueio por spam)
            if i < len(contatos):
                time.sleep(delay)

        # Relatório final
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL")
        print("=" * 60)
        print(f"✅ Emails enviados com sucesso: {enviados}")
        print(f"❌ Falhas no envio: {falhas}")
        print(f"📈 Taxa de sucesso: {(enviados/len(contatos)*100):.1f}%")
        print("=" * 60)


def main():
    """Função principal"""
    try:
        # Criar instância do sistema de email marketing
        email_system = EmailMarketingCEPEO()

        # Enviar campanha
        # Para teste, você pode limitar o número de emails:
        # email_system.enviar_campanha(limite=5)  # Envia apenas para 5 contatos

        # Para enviar para todos:
        email_system.enviar_campanha()

    except KeyboardInterrupt:
        print("\n\n⚠️  Processo interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
