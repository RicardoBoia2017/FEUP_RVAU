using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public GameObject[] enemies;
    private int numberEnemies = 0;
    private int maxEnemies = 100;
    private int enemiesDown = 0;
    private GameObject hero;
    private bool invokerCalled = false;
    public GameObject levelWonUI;
    public GameObject GameOverUI;

    void Start()
    {
        enemiesDown = 0;
    }
    public void InvokeSpawnEnemy()
    {
        if(!invokerCalled)
        {
            hero =  GameObject.Find("Hero"); 
            InvokeRepeating("SpawnEnemy", 3f, 1f);
            invokerCalled = true;
        }
    }

    void SpawnEnemy()
    {
        numberEnemies++;
        if(numberEnemies > maxEnemies)
            return;

        GameObject enemyPrefab;
        Transform enemyTransform;

        enemyPrefab = enemies[Random.Range(0,enemies.Length)];

        enemyTransform = enemyPrefab.transform;

/*      Vector3 origin = hero.transform.position; 
        float radius = 1f;

        Vector2 randomPos = Random.insideUnitCircle.normalized * radius;
        enemyTransform.position = origin + new Vector3(randomPos.x, 0, randomPos.y);


        enemyTransform.name = "Enemy #" + numberEnemies;
        Instantiate(enemyPrefab, enemyTransform);*/

/*      Make cubes spawn in front of hero*/
        
        Vector3 playerPos = hero.transform.position + new Vector3(0,0.07f,0);
        Vector3 playerDirection = hero.transform.forward;
        Quaternion playerRotation = enemyPrefab.transform.rotation;
        float spawnDistance = 1;

        Vector3 enemyPos = playerPos + playerDirection*spawnDistance;

        Instantiate(enemyPrefab, enemyPos, playerRotation);
    }

    public void EnemyDown()
    {
        enemiesDown++;
        if(enemiesDown >= maxEnemies)
            WinLevel();
    }

    void WinLevel()
    {
        enemiesDown = 0;
        numberEnemies = 0;
        invokerCalled = false;
        levelWonUI.SetActive(true);
    }
    public void GameOver(GameObject collider)
    {
        numberEnemies = maxEnemies;
        collider.GetComponent<EnemyBehaviour>().isCollider = true;

        GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
        foreach (GameObject enemy in enemies)
            if(enemy != collider)
                Destroy(enemy);
        Invoke("setUIActive", 1f);
    }

    private void setUIActive()
    {
        GameOverUI.SetActive(true);
    }

    public void GoToMenu()
    {
        SceneManager.LoadScene(0);
    }
}
