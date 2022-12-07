from tortoise import fields, models


class guilds(models.Model):
    id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField()
    host = fields.CharField(max_length=255, default="127.0.0.1")
    query_port = fields.CharField(max_length=255, default="25566")
    rcon_port = fields.CharField(max_length=255, default="25567")
    rcon_password = fields.CharField(max_length=255, default="123456")

    def __str__(self):
        return self.guild_id

    class Meta:
        table = "guilds"

