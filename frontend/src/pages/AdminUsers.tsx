import React, { useState, useEffect } from "react";
import { userService } from "../api/userService";
import type { User, UserCreate } from "../api/types";

const AdminUsers: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState({
    username: "",
    email: "",
    full_name: "",
    is_active: true,
    role: "user" as "user" | "engineer" | "admin",
  });
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createForm, setCreateForm] = useState({
    username: "",
    email: "",
    full_name: "",
    password: "",
    is_active: true,
    role: "user" as "user" | "engineer" | "admin",
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const usersData = await userService.getUsers();
      setUsers(usersData);
      setError("");
    } catch (err) {
      console.error("Ошибка загрузки пользователей:", err);
      setError("Не удалось загрузить список пользователей");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user: User) => {
    setEditingUserId(user.id);
    setEditForm({
      username: user.username,
      email: user.email,
      full_name: user.full_name || "",
      is_active: user.is_active,
      role: user.role,
    });
  };

  const handleCancelEdit = () => {
    setEditingUserId(null);
    setEditForm({
      username: "",
      email: "",
      full_name: "",
      is_active: true,
      role: "user",
    });
  };

  const handleSaveEdit = async () => {
    if (!editingUserId) return;

    try {
      await userService.updateUser(editingUserId, editForm);
      setEditingUserId(null);
      loadUsers(); // Обновляем список пользователей
    } catch (err) {
      console.error("Ошибка обновления пользователя:", err);
      setError("Не удалось обновить пользователя");
    }
  };

  const handleDelete = async (userId: number) => {
    if (window.confirm("Вы уверены, что хотите удалить этого пользователя?")) {
      try {
        await userService.deleteUser(userId);
        loadUsers(); // Обновляем список пользователей
      } catch (err) {
        console.error("Ошибка удаления пользователя:", err);
        setError("Не удалось удалить пользователя");
      }
    }
  };

  const handleRoleChange = (role: "user" | "engineer" | "admin") => {
    setEditForm((prev) => ({ ...prev, role }));
  };

  const handleCreateRoleChange = (role: "user" | "engineer" | "admin") => {
    setCreateForm((prev) => ({ ...prev, role }));
  };

  const handleCreateChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setCreateForm((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleCreateUser = async () => {
    try {
      await userService.createUser(createForm);
      setShowCreateForm(false);
      setCreateForm({
        username: "",
        email: "",
        full_name: "",
        password: "",
        is_active: true,
        role: "user",
      });
      loadUsers(); // Обновляем список пользователей
    } catch (err) {
      console.error("Ошибка создания пользователя:", err);
      setError("Не удалось создать пользователя");
    }
  };

  const toggleCreateForm = () => {
    setShowCreateForm(!showCreateForm);
  };

  if (loading) {
    return (
      <div className="admin-users-container">Загрузка пользователей...</div>
    );
  }

  return (
    <div className="admin-users-container">
      <h2>Управление пользователями</h2>

      {error && <div className="error-message">{error}</div>}

      <div className="admin-users-controls">
        <button className="add-btn" onClick={toggleCreateForm}>
          {showCreateForm ? "Отмена" : "Создать пользователя"}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-user-modal">
          <h3>Создание нового пользователя</h3>
          <div className="form-group">
            <label>Имя пользователя:</label>
            <input
              type="text"
              name="username"
              value={createForm.username}
              onChange={handleCreateChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={createForm.email}
              onChange={handleCreateChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Полное имя:</label>
            <input
              type="text"
              name="full_name"
              value={createForm.full_name}
              onChange={handleCreateChange}
            />
          </div>
          <div className="form-group">
            <label>Пароль:</label>
            <input
              type="password"
              name="password"
              value={createForm.password}
              onChange={handleCreateChange}
              required
            />
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={createForm.is_active}
                onChange={handleCreateChange}
              />
              Активен
            </label>
          </div>
          <div className="form-group">
            <label>Роль:</label>
            <select
              name="role"
              value={createForm.role}
              onChange={(e) => handleCreateRoleChange(e.target.value as "user" | "engineer" | "admin")}
            >
              <option value="user">Пользователь</option>
              <option value="engineer">Инженер</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
          <div className="modal-actions">
            <button className="save-btn" onClick={handleCreateUser}>
              Создать
            </button>
            <button className="cancel-btn" onClick={() => setShowCreateForm(false)}>
              Отмена
            </button>
          </div>
        </div>
      )}

      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя пользователя</th>
              <th>Email</th>
              <th>Полное имя</th>
              <th>Роль</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.full_name}</td>
                <td>
                  {user.role === "admin" && "Администратор"}
                  {user.role === "engineer" && "Инженер"}
                  {user.role === "user" && "Пользователь"}
                </td>
                <td>
                  {user.is_active ? (
                    <span className="status-active">Активен</span>
                  ) : (
                    <span className="status-inactive">Неактивен</span>
                  )}
                </td>
                <td>
                  <button className="edit-btn" onClick={() => handleEdit(user)}>
                    Редактировать
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(user.id)}
                  >
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {editingUserId && (
        <div className="edit-user-modal">
          <h3>Редактирование пользователя</h3>
          <div className="form-group">
            <label>Имя пользователя:</label>
            <input
              type="text"
              value={editForm.username}
              onChange={(e) =>
                setEditForm({ ...editForm, username: e.target.value })
              }
            />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={editForm.email}
              onChange={(e) =>
                setEditForm({ ...editForm, email: e.target.value })
              }
            />
          </div>
          <div className="form-group">
            <label>Полное имя:</label>
            <input
              type="text"
              value={editForm.full_name}
              onChange={(e) =>
                setEditForm({ ...editForm, full_name: e.target.value })
              }
            />
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={editForm.is_active}
                onChange={(e) =>
                  setEditForm({ ...editForm, is_active: e.target.checked })
                }
              />
              Активен
            </label>
          </div>
          <div className="form-group">
            <label>Роль:</label>
            <select
              value={editForm.role}
              onChange={(e) =>
                handleRoleChange(
                  e.target.value as "user" | "engineer" | "admin"
                )
              }
            >
              <option value="user">Пользователь</option>
              <option value="engineer">Инженер</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
          <div className="modal-actions">
            <button className="save-btn" onClick={handleSaveEdit}>
              Сохранить
            </button>
            <button className="cancel-btn" onClick={handleCancelEdit}>
              Отмена
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;
