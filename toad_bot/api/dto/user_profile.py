from dataclasses import dataclass
from datetime import datetime
from typing import Any

from toad_bot.enums import TaskTypeEnum


@dataclass
class TaskInfo:
    user_id: int
    task_type: TaskTypeEnum
    next_run: datetime
    turn: bool
    extra: dict[Any, Any]

    @staticmethod
    def load_from_json(data: dict[Any, Any]) -> "TaskInfo":
        return TaskInfo(
            user_id=data["user_id"],
            task_type=TaskTypeEnum(data["task_type"]),
            next_run=data["next_run"],
            turn=data["turn"],
            extra=data["extra"]
        )
    
    @staticmethod
    def load_from_jsons(data: list[dict[Any, Any]]) -> list["TaskInfo"]:
        return [
            TaskInfo(
                user_id=task["user_id"],
                task_type=TaskTypeEnum(task["task_type"]),
                next_run=datetime.fromisoformat(task["next_run"]),
                turn=task["turn"],
                extra=task["extra"]
            )
            for task in data
        ]


@dataclass
class UserInfo:
    id: int
    is_banned: bool
    is_vip: bool
    is_calculate: bool
    paid_until: datetime
    chat_id: int | None
    chat_title: str | None
    api_id: int | None
    api_hash: str | None
    phone: str | None
    password_2fa: str | None

    @staticmethod
    def load_from_json(data: dict[Any, Any]) -> "UserInfo":
        return UserInfo(
            id=data["id"],
            is_banned=data["is_banned"],
            is_vip=data["is_vip"],
            is_calculate=data["is_calculate"],
            paid_until=datetime.fromisoformat(data["paid_until"]),
            chat_id=data["chat_id"],
            chat_title=data["chat_title"],
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            phone=data["phone"],
            password_2fa=data["password_2fa"]
        )

@dataclass
class UserProfile:
    user: UserInfo
    tasks: list[TaskInfo]

    @staticmethod
    def load_from_json(data: dict[Any, Any]) -> "UserProfile":
        return UserProfile(
            user=UserInfo.load_from_json(data["user"]),
            tasks=TaskInfo.load_from_jsons(data["tasks"]["tasks"])
        )