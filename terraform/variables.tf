variable "youtube_api_key" {
  description = "YouTube Data API v3 key"
  type        = string
  sensitive   = true
}

variable "telegram_token" {
  description = "Telegram Bot token"
  type        = string
  sensitive   = true
}

variable "telegram_chat_id" {
  description = "Telegram Chat ID"
  type        = string
}
