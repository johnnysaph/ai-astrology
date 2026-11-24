"use client"

import * as ProgressPrimitive from "@radix-ui/react-progress"
import type { ComponentProps } from "react"

import { cn } from "@/lib/utils"

function Progress({ className, value = null, ...props }: ComponentProps<typeof ProgressPrimitive.Root>) {
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      className={cn("bg-primary/20 h-2 w-full overflow-hidden rounded-full", className)}
      value={value}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className={cn("bg-primary h-full w-full transition-transform", value === null && "motion-safe:animate-pulse")}
        style={{ transform: value === null ? undefined : `translateX(-${100 - value}%)` }}
      />
    </ProgressPrimitive.Root>
  )
}

export { Progress }
