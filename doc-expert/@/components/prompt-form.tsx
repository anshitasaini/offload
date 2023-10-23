import { PaperPlaneIcon } from "@radix-ui/react-icons"
import React from "react"
import Textarea from "react-textarea-autosize"

import { Button } from "./ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger
} from "./ui/tooltip"

const PromptForm = () => {
  // const { formRef, onKeyDown } = useEnterSubmit()
  const onKeyDown = () => {}

  const inputRef = React.useRef<HTMLTextAreaElement>(null)
  const [input, setInput] = React.useState("")

  return (
    <TooltipProvider>
      <div className="relative flex w-full grow flex-col overflow-hidden bg-background px-2 sm:rounded-md sm:border">
        <Textarea
          ref={inputRef}
          tabIndex={0}
          onKeyDown={onKeyDown}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message."
          spellCheck={false}
          className="min-h-[30px] w-full resize-none bg-transparent px-1 py-[0.8rem] focus-within:outline-none sm:text-sm"
        />
        <div className="absolute right-0 top-1 sm:right-2">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                type="submit"
                size="icon"
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
