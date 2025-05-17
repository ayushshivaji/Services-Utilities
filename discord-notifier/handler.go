package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
)

type PublishRequest struct {
	Message string `json:"message"`
}

func handlePublish(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error reading body: %v", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	var req PublishRequest
	if err := json.Unmarshal(body, &req); err != nil || req.Message == "" {
		log.Printf("Invalid JSON payload: %v", err)
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	webhookURL := os.Getenv("DISCORD_WEBHOOK_URL")
	if webhookURL == "" {
		log.Println("DISCORD_WEBHOOK_URL not set")
		http.Error(w, "Server config error", http.StatusInternalServerError)
		return
	}

	err = sendToDiscord(webhookURL, req.Message)
	if err != nil {
		log.Printf("Error sending to Discord: %v", err)
		http.Error(w, "Failed to publish message", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"message published"}`))
}
