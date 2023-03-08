# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    openapi_api_key = fields.Char(string="API Key", help="Provide the API key here", config_parameter="is_chatgpt_integration.openapi_api_key")
    openapi_model_name = fields.Selection(
        string="AI Model", 
        selection=[
            ('gpt-3.5-turbo', 'Chatgpt 3.5 Turbo'),
            ('gpt-3.5-turbo-0301', 'Chatgpt 3.5 Turbo on 20230301'),
            ('text-davinci-003', 'Chatgpt 3 Davinci'),
            ('code-davinci-002', 'Chatgpt 2 Code Optimized'),
            ('text-davinci-002', 'Chatgpt 2 Davinci'),
            # ('dall-e2', 'Dall-E Image'),
        ], 
        required=True, 
        default='gpt-3.5-turbo',
        help="""
            GPT-3.5: A set of models that improve on GPT-3 and can understand as well as generate natural language or code
            DALL·E: A model that can generate and edit images given a natural language prompt
            Whisper: A model that can convert audio into text
            Embeddings:	A set of models that can convert text into a numerical form
            CodexLimited: A set of models that can understand and generate code, including translating natural language to code
            Moderation: A fine-tuned model that can detect whether text may be sensitive or unsafe
            GPT-3	A set of models that can understand and generate natural language
        """,
        config_parameter="is_chatgpt_integration.openapi_model_name"
    )
