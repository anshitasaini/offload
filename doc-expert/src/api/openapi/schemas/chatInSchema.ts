/**
 * Generated by orval v6.19.1 🍺
 * Do not edit manually.
 * FastAPI
 * OpenAPI spec version: 0.1.0
 */
import type { ChatMessageSchema } from "./chatMessageSchema"

export type ChatInSchema = {
  current_url: string
  history: ChatMessageSchema[]
  query: string
}
