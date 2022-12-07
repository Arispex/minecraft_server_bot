from mcstatus import JavaServer
import mcrcon
import models


class Server:
    """
    服务器对象
    """

    @classmethod
    async def get(cls, guild_id: int) -> 'Server':
        """
        获取服务器对象
        :param guild_id: 服务器所在的服务器ID
        :return: 服务器对象
        """
        guild = await models.orm.guilds.get(guild_id=guild_id)
        return cls(guild.host, guild.query_port, guild.rcon_port, guild.rcon_password)

    def __init__(self, host: str, query_port: int, rcon_port: int, rcon_password: str):
        """
        初始化
        :param host: 主机地址
        :param query_port: 查询端口
        :param rcon_port: 远程指令端口
        :param rcon_password: 远程指令密码
        """
        self.host = host
        self.query_port = query_port
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

        self.query = JavaServer.lookup(f"{host}:{query_port}", timeout=1)

        self.rcon = mcrcon.MCRcon(host=host, port=rcon_port, password=rcon_password, timeout=1)

    def command(self, cmd: str) -> str:
        """
        远程指令
        :param cmd: 指令内容
        :return: 返回结果
        """
        return self.rcon.command(cmd)
