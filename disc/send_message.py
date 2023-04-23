from discord import Interaction, ApplicationContext

MAX_MESSAGE_LENGTH = 1950


async def send_message(ctx: ApplicationContext, message: str):
    def find_boundary(message_part: str, index: int) -> tuple[int, bool]:
        code_block_marker = "```"

        in_code_block = False
        for i in range(index - len(code_block_marker) + 1):
            if message_part[i:i + len(code_block_marker)] == code_block_marker:
                in_code_block = not in_code_block

        if in_code_block:
            opening_code_block = message_part.rfind(code_block_marker, 0, index)
            if opening_code_block != -1:
                return opening_code_block, True
        return index, in_code_block

    def split_message(message: str, max_length: int) -> list[str]:
        message_parts = []
        start = 0
        in_code_block = False

        message_part = ""
        while start < len(message):
            if len(message) - start <= max_length:
                end = len(message)
            else:
                end = start + max_length
                end, in_code_block = find_boundary(message, end)

            message_part += message[start:end]

            if in_code_block:
                message_part += "```"

            message_parts.append(message_part)
            start = end

            if in_code_block:
                message_part = "```"
            else:
                message_part = ""

        return message_parts

    message_parts = split_message(message, MAX_MESSAGE_LENGTH)
    for message_part in message_parts:
        await ctx.respond(message_part)
