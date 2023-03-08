# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

import openai

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
        user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
        partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')
        if not prompt:
            return rdata
        openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
        openapi_model_name = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_model_name')
        Partner = self.env['res.partner']
        partner_name = ''
        if author_id:
            partner_id = Partner.browse(author_id)
            if partner_id:
                partner_name = partner_id.name
        if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
            try:
                if openapi_model_name not in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301"]:
                    response = openai.Completion.create(
                        model=openapi_model_name,
                        prompt=prompt,
                        temperature=0.6,
                        max_tokens=3000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        user = partner_name,
                    )
                    res = response['choices'][0]['text']
                else:
                    response = openai.ChatCompletion.create(
                        model=openapi_model_name, 
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.9,
                        max_tokens=2048,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        user=partner_name,
                    )
                    res = response.choices[0].message.content
                res = res.strip().replace('\n', '<br/>')
                self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
            try:
                if openapi_model_name not in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301"]:
                    response = openai.Completion.create(
                        model=openapi_model_name,
                        prompt=prompt,
                        temperature=0.6,
                        max_tokens=3000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        user = partner_name,
                    )
                    res = response['choices'][0]['text']
                else:
                    response = openai.ChatCompletion.create(
                        model=openapi_model_name, 
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.9,
                        max_tokens=2048,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        user=partner_name,
                    )
                    res = response.choices[0].message.content
                res = res.strip().replace('\n', '<br/>')
                chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        return rdata
