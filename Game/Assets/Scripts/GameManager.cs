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
    private List<int> odds;
    void Start()
    {
        enemiesDown = 0;
        string sceneName = SceneManager.GetActiveScene().name;

        if(sceneName == "Game")
            odds = new List<int> {0,0,0,0,0,0,0,0,0,0};
        else if(sceneName == "Level 2")
            odds = new List<int> {0,0,0,0,0,0,0,1,1,1};
        else if(sceneName == "Level 3")
            odds = new List<int> {0,0,0,0,0,1,1,1,1,1};
        else if(sceneName == "Level 4")
            odds = new List<int> {0,0,0,1,1,1,1,1,1,2};
        else if(sceneName == "Level 5")
            odds = new List<int> {0,0,1,1,1,1,1,2,2,2};
    }

    public void InvokeSpawnEnemy()
    {
        if(!invokerCalled)
        {
            hero =  GameObject.Find("Hero"); 
            InvokeRepeating("SpawnEnemy", 3f, 0.1f);
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

        int index = Random.Range(0,10);
        enemyPrefab = enemies[odds[index]];
        Debug.Log(odds[index]);
        return;
        Quaternion randAng = Quaternion.Euler(0, Random.Range(-20,20), 0);
        randAng = hero.transform.rotation * randAng; // this might be backwards
        Vector3 spawnPos = hero.transform.position + randAng * Vector3.forward;

        Instantiate(enemyPrefab, spawnPos - new Vector3(0,0,0.3f), enemyPrefab.transform.rotation);
/*        

        enemyTransform = enemyPrefab.transform;

        Vector3 origin = hero.transform.position; 
        float radius = 1f;

        Vector2 randomPos = Random.insideUnitCircle.normalized * radius;
        enemyTransform.position = origin + new Vector3(randomPos.x, 0, randomPos.y);

        Instantiate(enemyPrefab, enemyTransform);*/

/*      Make cubes spawn in front of hero*/
        
        /*Vector3 playerPos = hero.transform.position + new Vector3(0,0.07f,0);
        Vector3 playerDirection = hero.transform.forward;
        Quaternion playerRotation = enemyPrefab.transform.rotation;
        float spawnDistance = 1;

        Vector3 enemyPos = playerPos + playerDirection*spawnDistance;

        Instantiate(enemyPrefab, enemyPos, playerRotation);*/
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
