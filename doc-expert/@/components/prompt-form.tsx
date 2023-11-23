import { PaperPlaneIcon } from "@radix-ui/react-icons"
import React from "react"
import Textarea from "react-textarea-autosize"

import { chatSendMessage } from "~api/openapi/chat/chat"
import type { ChatMessageSchema } from "~api/openapi/schemas"

import { Button } from "./ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger
} from "./ui/tooltip"

export interface PromptFormProps {
  sendMessage: (message: string) => void
}

const PromptForm = ({ sendMessage }: PromptFormProps) => {
  const [input, setInput] = React.useState("")

  const onKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault()
      setInput("")
      sendMessage(input)
    }
  }

  const inputRef = React.useRef<HTMLTextAreaElement>(null)

  return (
    <TooltipProvider>
      <div className="relative flex w-full grow overflow-hidden bg-background px-4 py-1 sm:rounded-md sm:border items-center">
        <Textarea
          ref={inputRef}
          tabIndex={0}
          onKeyDown={onKeyDown}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="How do I get started?"
          spellCheck={false}
          className="min-h-[30px] w-full resize-none bg-transparent px-1 py-[0.8rem] focus-within:outline-none sm:text-sm"
        />
        <div className="">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                type="submit"
                size="icon"
                variant="ghost"
                disabled={input === ""}>
                <PaperPlaneIcon />
                <span className="sr-only">Send message</span>
              </Button>
            </TooltipTrigger>
            <TooltipContent>Send message</TooltipContent>
          </Tooltip>
        </div>
      </div>
    </TooltipProvider>
  )
}

export default PromptForm
