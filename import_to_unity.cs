using System;
using System.IO;
using UnityEngine;

public class LevelLoader : MonoBehaviour
{
    public GameObject platformPrefab; // Префаб платформы
    public string levelFile = "Assets/level.txt"; // Путь к файлу уровня
    public float blockSize = 1f; // Размер одного блока

    void Start()
    {
        LoadLevel();
    }

    void LoadLevel()
    {
        if (!File.Exists(levelFile))
        {
            Debug.LogError("Файл уровня не найден: " + levelFile);
            return;
        }

        string[] lines = File.ReadAllLines(levelFile);
        int height = lines.Length;
        int width = lines[0].Length;

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                if (lines[height - y - 1][x] == '1') // '1' соответствует платформе
                {
                    Vector3 position = new Vector3(x * blockSize, y * blockSize, 0);
                    Instantiate(platformPrefab, position, Quaternion.identity);
                }
            }
        }

        Debug.Log("Уровень успешно загружен!");
    }
}
