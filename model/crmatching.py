import torch.nn as nn

from model.basic_dialog_model import BasicDialogModel


class CRMatchingModel(BasicDialogModel):

    def _init_main_task(self):
        self.matching_cls = nn.Sequential(nn.Dropout(p=self.args.dropout_rate),
                                 nn.Linear(self.model_config.hidden_size, 1))
        self.matching_loss_fct = nn.BCEWithLogitsLoss()        

    def main_forward(self, token_ids, segment_ids, attention_mask, label):
        outputs = self.model(input_ids=token_ids,
                             attention_mask=attention_mask,
                             token_type_ids=segment_ids)
        cls_hidden = outputs.last_hidden_state[:, 0, :] # [batch_size, hidden]
        logits = self.matching_cls(cls_hidden).squeeze(-1) # [batch_size,]
        loss = self.matching_loss_fct(logits, label)
        return logits, loss
