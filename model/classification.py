import torch.nn as nn

from model.basic_dialog_model import BasicDialogModel


class ClassificationModel(BasicDialogModel):

    def _init_main_task(self):
        self.cls = nn.Sequential(nn.Dropout(p=self.args.dropout_rate),
                                 nn.Linear(self.model_config.hidden_size,
                                           self.args.n_class))
        self.cls_loss_fct = nn.CrossEntropyLoss()        

    def main_forward(self, token_ids, segment_ids, attention_mask, label):
        outputs = self.model(input_ids=token_ids,
                             attention_mask=attention_mask,
                             token_type_ids=segment_ids)
        cls_hidden = outputs.last_hidden_state[:, 0, :] # [batch_size, hidden]
        logits = self.cls(cls_hidden) # [batch_size, n_class]
        loss = self.cls_loss_fct(logits, label.long())
        return logits, loss
        