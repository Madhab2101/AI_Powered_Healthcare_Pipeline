# 🩺 AI-Powered Predictive Healthcare Data Pipeline using Kafka and Spark

A real-time **AI-driven healthcare analytics pipeline** that continuously streams patient vital signs, processes them using **Apache Kafka** and **Apache Spark Structured Streaming**, predicts health risk levels (**High / Medium / Low**) using an **AI model (Random Forest)** served via **FastAPI**, and visualizes the results in a live **Streamlit dashboard**.

---

## 🚀 **Overview**

This project demonstrates how real-time healthcare data can be processed and analyzed using distributed technologies and AI.  
It integrates a **streaming pipeline** for patient monitoring, applying **AI-based health risk forecasting** in real-time.

---

## 🧠 **System Architecture**

```text
[Data Simulator] → [Kafka Producer] → [Kafka Topic: raw-patient]
                        ↓
                [Spark Structured Streaming ETL]
                        ↓
                [Cleaned Parquet Data Storage]
                        ↓
                  [FastAPI AI Model Server]
                        ↓
                [Streamlit Real-Time Dashboard]
