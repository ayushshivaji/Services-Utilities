package main

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type DiscordPayload struct {
	Content string `json:"content"`
}

func sendToDiscord(webhookURL, message string) error {
	payload := DiscordPayload{Content: message}

	body, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(body))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		return err
	}

	return nil
}
